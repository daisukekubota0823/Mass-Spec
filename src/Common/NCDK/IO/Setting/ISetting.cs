/*
 * Copyright (C) 2012 John May <jwmay@users.sf.net>
 *
 * Contact: cdk-devel@lists.sourceforge.net
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public License
 * as published by the Free Software Foundation; either version 2.1
 * of the License, or (at your option) any later version.
 * All we ask is that proper credit is given for our work, which includes
 * - but is not limited to - adding the above copyright notice to the beginning
 * of your source code files, and to any copyright notice that you may distribute
 * with programs based on this work.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT Any WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA.
 */

namespace NCDK.IO.Setting
{
    /// <summary>
    /// A simple setting that can be managed by the SettingManager.Currently the only
    /// required method is <see cref="Name"/> and provides the key with which setting are
    /// added and retrieved with.    
    /// </summary>
    /// <seealso cref="SettingManager{T}"/>
    // @author      johnmay
    // @cdk.created 20.03.2012
    public interface ISetting
    {
        /// <summary>
        /// The name of the setting.
        /// </summary>
        string Name { get; }
    }
}
